#include <iostream>

using namespace std;

/*
==========================================================================
 1. NODO Y LISTA DOBLEMENTE ENLAZADA
    - head: Elemento más recientemente usado (MRU)
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

        // Desconectar nodo de su posición actual
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

    // Elimina el último elemento (LRU) y retorna su clave - O(1)
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

    // Imprime el estado de la caché de MRU (head) a LRU (tail)
    void print_cache() const {
        DoubleNode<K, V> *curr = head;
        cout << "[ Head/MRU: ";
        while (curr != nullptr) {
            cout << "(" << curr->key << ":" << curr->value << ")";
            if (curr->next != nullptr) cout << " -> ";
            curr = curr->next;
        }
        cout << " :Tail/LRU ]\n";
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

    // Búsqueda en O(1) promedio del puntero al nodo
    DoubleNode<int, int>* get(int k) const {
        int p = hash(k);
        HashNode *temp = buckets[p];
        while (temp != nullptr) {
            if (temp->key == k) return temp->node_ptr;
            temp = temp->next;
        }
        return nullptr;
    }

    // Inserción o actualización de la referencia
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

    // Eliminación de una clave de la tabla hash
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
 3. LRU CACHE
==========================================================================
*/
class LRUCache {
private:
    int capacity;
    DoubleLinkedList<int, int> list; // Mantiene el orden de uso (MRU -> LRU)
    Dictionary map;                  // Acceso O(1): key -> nodo

public:
    LRUCache(int cap) : capacity(cap), map(cap * 2) {}

    // Obtener valor: O(1)
    int get(int key) {
        DoubleNode<int, int> *node = map.get(key);
        if (node == nullptr) {
            return -1; // No encontrado (Cache Miss)
        }

        // Cache Hit: mover al inicio (MRU)
        list.move_to_front(node);
        return node->value;
    }

    // Insertar o actualizar valor: O(1)
    void put(int key, int value) {
        if (capacity <= 0) return;

        DoubleNode<int, int> *node = map.get(key);

        if (node != nullptr) {
            // Clave existente: actualizar valor y mover al frente (MRU)
            node->value = value;
            list.move_to_front(node);
        } else {
            // Clave nueva: verificar capacidad
            if (list.size() >= capacity) {
                // Desalojar el menos recientemente usado (LRU al final)
                int evicted_key = list.pop_back();
                map.erase(evicted_key);
                cout << "   [EVICCION] Se expulso la clave LRU: " << evicted_key << "\n";
            }

            // Insertar nuevo nodo al inicio y registrar en la tabla hash
            DoubleNode<int, int> *new_node = list.push_front(key, value);
            map.insert(key, new_node);
        }
    }

    void display() const {
        list.print_cache();
    }
};

/*
==========================================================================
 4. CASO DE PRUEBA EN MAIN
==========================================================================
*/
int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    int capacidad = 3;
    cout << "=== CREANDO LRU CACHE CON CAPACIDAD = " << capacidad << " ===\n\n";
    LRUCache cache(capacidad);

    cout << "1. Insertando (1, 10), (2, 20), (3, 30):\n";
    cache.put(1, 10);
    cache.put(2, 20);
    cache.put(3, 30);
    cache.display();
    cout << "\n";

    cout << "2. Consultando get(1) [Cache Hit]:\n";
    int val = cache.get(1);
    cout << "   Valor obtenido: " << val << "\n";
    cout << "   -> El elemento 1 debe haberse movido al frente (MRU):\n   ";
    cache.display();
    cout << "\n";

    cout << "3. Insertando (4, 40) con la cache llena:\n";
    cout << "   -> Debe expulsar la clave 2 (LRU al final de la lista)\n";
    cache.put(4, 40);
    cache.display();
    cout << "\n";

    cout << "4. Verificando que la clave 2 ya no existe:\n";
    cout << "   get(2): " << cache.get(2) << " (-1 indica Cache Miss)\n\n";

    cout << "5. Actualizando valor de una clave existente put(3, 99):\n";
    cache.put(3, 99);
    cout << "   -> Debe actualizarse a 99 y moverse al Head:\n   ";
    cache.display();
    cout << "\n";

    cout << "6. Insertando (5, 50) para forzar otro desalojo:\n";
    cout << "   -> Debe expulsar la clave 1 (actual LRU)\n";
    cache.put(5, 50);
    cache.display();

    return 0;
}