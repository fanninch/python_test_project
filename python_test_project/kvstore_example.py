from python_test_project.kvstore import StoreConfig, create_store, KeyValueStore, KeyNotFound

if __name__ == "__main__":

    cfg = StoreConfig(backend="memory", default_ttl=5)
    store: KeyValueStore = create_store(cfg)

    store.set("users/alice", b"hello")
    print(store.get("users/alice"))                 # b'hello'
    print(list(store.list("users/")))               # ['users/alice']
    print(store.delete("users/alice"))              # True

    try:
        store.get("missing")
    except KeyNotFound:
        print("Key not found")

    store.close()