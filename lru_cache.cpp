#include <iostream>

using namespace std;

/*
==========================================================================
 CAMBIOS RESPECTO A LA VERSION ANTERIOR
   - DoubleLinkedList, HashNode y Dictionary NO cambian (misma logica).
   - Se agrega la clase Trace: escribe un evento JSON por cada paso real
     de get/put (HASH, PROBE, HIT, MISS, UPDATE, MOVE_TO_FRONT, EVICT,
     INSERT) y el estado completo (lista + buckets) al terminar la operacion.
   - LRUCache ya no imprime nada con cout: si el trace esta activo, emite
     eventos; si no, se comporta igual que antes.
   - El main ejecuta varios escenarios (incluidos los casos borde) y
     verifica resultados con CHECK. La salida estandar es el trace (JSONL).
==========================================================================
*/

/*
==========================================================================
 1. NODO Y LISTA DOBLEMENTE ENLAZADA
    - head: Elemento mas recientemente usado (MRU)
    - tail: Elemento menos recientemente usado (LRU)
==========================================================================
*/
template<typename K, typename V>
struct DoubleNode {
    K key;
    V value;
    DoubleNode<K, V> *next;
    DoubleNode<K, V> *prev;

    DoubleNode(K k, V v) : key(k), value(v), next(nullptr), prev(nullptr) {}
};

template<typename K, typename V>
struct DoubleLinkedList {
    DoubleNode<K, V> *head = nullptr;
    DoubleNode<K, V> *tail = nullptr;
    int n = 0;

    bool empty() const { return n == 0; }
    int size() const { return n; }

    // Inserta un nodo nuevo al frente (MRU) - O(1)
    DoubleNode<K, V>* push_front(K key, V val) {
        DoubleNode<K, V> *new_node = new DoubleNode<K, V>(key, val);
        if (head == nullptr) {
            head = tail = new_node;
        } else {
            new_node->next = head;
            head->prev = new_node;
            head = new_node;
        }
        n++;
        return new_node;
    }

    // Mueve un nodo existente directamente al frente (MRU) - O(1)
    void move_to_front(DoubleNode<K, V> *node) {
        if (node == nullptr || node == head) return;

        // Desconectar nodo de su posicion actual
        if (node == tail) {
            tail = node->prev;
            tail->next = nullptr;
        } else {
            node->prev->next = node->next;
            node->next->prev = node->prev;
        }

        // Conectar como nueva cabeza
        node->prev = nullptr;
        node->next = head;
        head->prev = node;
        head = node;
    }

    // Elimina el ultimo elemento (LRU) y retorna su clave - O(1)
    K pop_back() {
        if (tail == nullptr) return K();

        DoubleNode<K, V> *temp = tail;
        K removed_key = temp->key;

        if (head == tail) {
            head = tail = nullptr;
        } else {
            tail = tail->prev;
            tail->next = nullptr;
        }

        delete temp;
        n--;
        return removed_key;
    }

    // Libera la memoria de toda la lista
    void clear() {
        DoubleNode<K, V> *curr = head;
        while (curr != nullptr) {
            DoubleNode<K, V> *sig = curr->next;
            delete curr;
            curr = sig;
        }
        head = tail = nullptr;
        n = 0;
    }

    ~DoubleLinkedList() {
        clear();
    }
};

/*
==========================================================================
 2. TABLA HASH (DICTIONARY)
    - Mapea: key -> DoubleNode<int, int>*
==========================================================================
*/
struct HashNode {
    int key;
    DoubleNode<int, int> *node_ptr;
    HashNode *next;

    HashNode(int _key, DoubleNode<int, int> *_node_ptr)
        : key(_key), node_ptr(_node_ptr), next(nullptr) {}
};

bool es_primo(int x) {
    if (x < 2) return false;
    for (int i = 2; (long long)i * i <= x; i++) {
        if (x % i == 0) return false;
    }
    return true;
}

int siguiente_primo(int x) {
    while (!es_primo(x)) {
        x++;
    }
    return x;
}

struct Dictionary {
    int m;
    int size;
    HashNode **buckets;

    Dictionary(int capacidad_inicial = 17) {
        m = siguiente_primo(capacidad_inicial);
        size = 0;
        buckets = new HashNode*[m];
        for (int i = 0; i < m; i++) buckets[i] = nullptr;
    }

    ~Dictionary() {
        clear();
        delete[] buckets;
    }

    int hash(int k) const {
        return ((unsigned int)k) % m;
    }

    float load_factor() const {
        return (float)size / m;
    }

    // Busqueda en O(1) promedio del puntero al nodo
    DoubleNode<int, int>* get(int k) const {
        int p = hash(k);
        HashNode *temp = buckets[p];
        while (temp != nullptr) {
            if (temp->key == k) return temp->node_ptr;
            temp = temp->next;
        }
        return nullptr;
    }

    // Insercion o actualizacion de la referencia
    void insert(int k, DoubleNode<int, int> *node_ptr) {
        if (load_factor() >= 0.75f) {
            rehashing();
        }

        int p = hash(k);
        HashNode *temp = buckets[p];
        while (temp != nullptr) {
            if (temp->key == k) {
                temp->node_ptr = node_ptr;
                return;
            }
            temp = temp->next;
        }

        HashNode *new_node = new HashNode(k, node_ptr);
        new_node->next = buckets[p];
        buckets[p] = new_node;
        size++;
    }

    // Eliminacion de una clave de la tabla hash
    bool erase(int k) {
        int p = hash(k);
        HashNode *temp = buckets[p];
        HashNode *prev = nullptr;

        while (temp != nullptr) {
            if (temp->key == k) {
                if (prev == nullptr) {
                    buckets[p] = temp->next;
                } else {
                    prev->next = temp->next;
                }
                delete temp;
                size--;
                return true;
            }
            prev = temp;
            temp = temp->next;
        }
        return false;
    }

    void clear() {
        for (int i = 0; i < m; i++) {
            HashNode *temp = buckets[i];
            while (temp != nullptr) {
                HashNode *sig = temp->next;
                delete temp;
                temp = sig;
            }
            buckets[i] = nullptr;
        }
        size = 0;
    }

    void rehashing() {
        int old_m = m;
        m = siguiente_primo(2 * m);
        HashNode **old_buckets = buckets;
        buckets = new HashNode*[m];

        for (int i = 0; i < m; i++) buckets[i] = nullptr;

        for (int i = 0; i < old_m; i++) {
            HashNode *temp = old_buckets[i];
            while (temp != nullptr) {
                HashNode *sig = temp->next;
                int nuevo_idx = hash(temp->key);
                temp->next = buckets[nuevo_idx];
                buckets[nuevo_idx] = temp;
                temp = sig;
            }
        }
        delete[] old_buckets;
    }
};

/*
==========================================================================
 3. TRACE (registro de eventos en formato JSON Lines)
    Una linea por operacion:
      {"scenario":..,"type":"op","op":"put","key":4,"value":40,
       "steps":[{"e":"HASH",...},...],"result":null,
       "list":[[k,v],...],          <- de MRU (head) a LRU (tail)
       "buckets":[[k,...],...]}     <- claves de cada bucket, en orden de cadena
    Si out == nullptr, todos los metodos no hacen nada.
==========================================================================
*/
const int NIL = -1000000; // "sin valor" -> se imprime como null

struct Trace {
    ostream *out = nullptr;
    const char *scenario = "";
    bool first_step = true;

    void sep() {
        if (!first_step) *out << ",";
        first_step = false;
    }
    void num(int v) {
        if (v == NIL) *out << "null"; else *out << v;
    }

    void state(const DoubleLinkedList<int, int> &list, const Dictionary &map) {
        *out << "\"list\":[";
        for (DoubleNode<int, int> *c = list.head; c != nullptr; c = c->next) {
            *out << "[" << c->key << "," << c->value << "]";
            if (c->next != nullptr) *out << ",";
        }
        *out << "],\"buckets\":[";
        for (int i = 0; i < map.m; i++) {
            *out << "[";
            for (HashNode *h = map.buckets[i]; h != nullptr; h = h->next) {
                *out << h->key;
                if (h->next != nullptr) *out << ",";
            }
            *out << "]";
            if (i + 1 < map.m) *out << ",";
        }
        *out << "]";
    }

    void init(const char *name, int capacity, const DoubleLinkedList<int, int> &list, const Dictionary &map) {
        scenario = name;
        if (!out) return;
        *out << "{\"scenario\":\"" << scenario << "\",\"type\":\"init\",\"capacity\":" << capacity
             << ",\"m\":" << map.m << ",";
        state(list, map);
        *out << "}\n";
    }

    void begin(const char *op, int key, int value) {
        if (!out) return;
        first_step = true;
        *out << "{\"scenario\":\"" << scenario << "\",\"type\":\"op\",\"op\":\"" << op
             << "\",\"key\":" << key << ",\"value\":";
        num(value);
        *out << ",\"steps\":[";
    }

    void step(const char *e) {
        if (!out) return;
        sep();
        *out << "{\"e\":\"" << e << "\"}";
    }
    void step(const char *e, const char *n1, int v1) {
        if (!out) return;
        sep();
        *out << "{\"e\":\"" << e << "\",\"" << n1 << "\":"; num(v1); *out << "}";
    }
    void step(const char *e, const char *n1, int v1, const char *n2, int v2) {
        if (!out) return;
        sep();
        *out << "{\"e\":\"" << e << "\",\"" << n1 << "\":"; num(v1);
        *out << ",\"" << n2 << "\":"; num(v2); *out << "}";
    }
    void probe(int k, bool match) {
        if (!out) return;
        sep();
        *out << "{\"e\":\"PROBE\",\"key\":" << k << ",\"match\":" << (match ? "true" : "false") << "}";
    }
    void move(int key, int prev, int next, int old_head, bool was_tail) {
        if (!out) return;
        sep();
        *out << "{\"e\":\"MOVE_TO_FRONT\",\"key\":" << key << ",\"prev\":"; num(prev);
        *out << ",\"next\":"; num(next);
        *out << ",\"old_head\":"; num(old_head);
        *out << ",\"was_tail\":" << (was_tail ? "true" : "false") << "}";
    }

    void end(const DoubleLinkedList<int, int> &list, const Dictionary &map, int result) {
        if (!out) return;
        *out << "],\"result\":"; num(result); *out << ",";
        state(list, map);
        *out << "}\n";
    }
};

/*
==========================================================================
 4. LRU CACHE
==========================================================================
*/
class LRUCache {
private:
    int capacity;
    DoubleLinkedList<int, int> list; // Mantiene el orden de uso (MRU -> LRU)
    Dictionary map;                  // Acceso O(1): key -> nodo
    Trace trace;

    LRUCache(const LRUCache&) = delete;            // evita doble liberacion
    LRUCache& operator=(const LRUCache&) = delete;

    // Solo para el trace: HASH + recorrido de la cadena del bucket
    void trace_lookup(int key) {
        if (!trace.out) return;
        int b = map.hash(key);
        trace.step("HASH", "key", key, "bucket", b);
        for (HashNode *h = map.buckets[b]; h != nullptr; h = h->next) {
            bool match = (h->key == key);
            trace.probe(h->key, match);
            if (match) break;
        }
    }

    // Solo para el trace: se llama ANTES de list.move_to_front(node)
    void trace_move(DoubleNode<int, int> *node) {
        if (!trace.out) return;
        if (node == list.head) {
            trace.step("ALREADY_HEAD", "key", node->key);
            return;
        }
        int prev = node->prev ? node->prev->key : NIL;
        int next = node->next ? node->next->key : NIL;
        trace.move(node->key, prev, next, list.head->key, node == list.tail);
    }

public:
    LRUCache(int cap) : capacity(cap), map(cap * 2) {}

    void enable_trace(ostream *out, const char *scenario_name) {
        trace.out = out;
        trace.init(scenario_name, capacity, list, map);
    }

    // Obtener valor: O(1) promedio
    int get(int key) {
        trace.begin("get", key, NIL);
        trace_lookup(key);

        DoubleNode<int, int> *node = map.get(key);
        if (node == nullptr) {
            trace.step("MISS");
            trace.end(list, map, -1);
            return -1; // No encontrado (Cache Miss)
        }

        // Cache Hit: mover al inicio (MRU)
        trace.step("HIT", "key", key);
        trace_move(node);
        list.move_to_front(node);
        trace.end(list, map, node->value);
        return node->value;
    }

    // Insertar o actualizar valor: O(1) promedio
    void put(int key, int value) {
        if (capacity <= 0) return;

        trace.begin("put", key, value);
        trace_lookup(key);
        DoubleNode<int, int> *node = map.get(key);

        if (node != nullptr) {
            // Clave existente: actualizar valor y mover al frente (MRU)
            trace.step("UPDATE", "key", key, "value", value);
            node->value = value;
            trace_move(node);
            list.move_to_front(node);
        } else {
            // Clave nueva: verificar capacidad
            if (list.size() >= capacity) {
                // Desalojar el menos recientemente usado (LRU al final)
                int lru_key = list.tail->key;
                trace.step("EVICT", "key", lru_key, "bucket", map.hash(lru_key));
                int evicted_key = list.pop_back();
                map.erase(evicted_key);
            }

            // Insertar nuevo nodo al inicio y registrar en la tabla hash
            DoubleNode<int, int> *new_node = list.push_front(key, value);
            map.insert(key, new_node);
            trace.step("INSERT", "key", key, "bucket", map.hash(key));
        }
        trace.end(list, map, NIL);
    }

    int size() const { return list.size(); }
};

/*
==========================================================================
 5. ESCENARIOS (cada uno genera su parte del trace) + verificaciones
==========================================================================
*/
#define CHECK(cond) do { if (!(cond)) { \
    cerr << "FALLO: " #cond " (linea " << __LINE__ << ")\n"; return 1; } } while (0)

int main() {
    ios_base::sync_with_stdio(false);
    ostream *out = &cout; // el trace va a la salida estandar

    // --- Escenario 1: caso principal (bloque 9 del guion) ---
    {
        LRUCache c(3);
        c.enable_trace(out, "principal");
        c.put(1, 10); c.put(2, 20); c.put(3, 30);      // lista: 3,2,1
        int r1 = c.get(1);                             // hit sobre la COLA -> 1,3,2
        CHECK(r1 == 10);
        c.put(4, 40);                                  // evicta la clave 2 -> 4,1,3
        int r2 = c.get(2);                             // miss
        CHECK(r2 == -1);
        CHECK(c.size() == 3);
    }

    // --- Escenario 2: punteros con un nodo INTERMEDIO (bloque 7) ---
    {
        LRUCache c(3);
        c.enable_trace(out, "punteros");
        c.put(1, 10); c.put(2, 20); c.put(3, 30);      // lista: 3,2,1
        int r = c.get(2);                              // nodo intermedio -> 2,3,1
        CHECK(r == 20);
    }

    // --- Casos borde (bloque 10) ---
    // Cache vacia
    {
        LRUCache c(3);
        c.enable_trace(out, "vacia");
        int r = c.get(5);
        CHECK(r == -1);
        CHECK(c.size() == 0);
    }
    // Capacidad 1: head == tail; cada put nuevo expulsa al anterior
    {
        LRUCache c(1);
        c.enable_trace(out, "capacidad1");
        c.put(1, 10);
        c.put(2, 20);                                  // evicta la clave 1
        int r1 = c.get(1);
        CHECK(r1 == -1);
        int r2 = c.get(2);                             // ya es head: no hay movimiento
        CHECK(r2 == 20);
        CHECK(c.size() == 1);
    }
    // put sobre clave existente: actualiza valor, sin duplicar ni expulsar
    {
        LRUCache c(3);
        c.enable_trace(out, "actualizar");
        c.put(1, 10); c.put(2, 20); c.put(3, 30);      // lista: 3,2,1
        c.put(1, 99);                                  // 1,3,2 (sin desalojo)
        CHECK(c.size() == 3);
        int r = c.get(1);
        CHECK(r == 99);
    }
    // Colision en la tabla: con capacidad 3, m = 7 -> 1 % 7 == 8 % 7 == 1
    {
        LRUCache c(3);
        c.enable_trace(out, "colision");
        c.put(1, 10);
        c.put(8, 80);                                  // mismo bucket que la clave 1
        int r1 = c.get(1);                             // recorre la cadena: 8 -> 1
        CHECK(r1 == 10);
        int r2 = c.get(8);
        CHECK(r2 == 80);
    }

    cerr << "Todas las verificaciones pasaron. Trace generado.\n";
    return 0;
}
