### HashMap

#### threshold的计算逻辑
> 保证map的容量为2的幂

```java
    // 9 -> 1001
    static final int tableSizeFor(int cap) {
        int n = cap - 1; // n = 8 1000
        n |= n >>> 1; // n = 1000 | 0100 = 1100
        n |= n >>> 2; // n = 1100 | 0011 = 1111
        n |= n >>> 4; // n = 1111 | 0000 = 1111
        n |= n >>> 8;
        n |= n >>> 16;
        return (n < 0) ? 1 : (n >= MAXIMUM_CAPACITY) ? MAXIMUM_CAPACITY : n + 1; // return 16 10000
    }


    // 32 -> 100000
    static final int tableSizeFor(int cap) {
        int n = cap - 1; // 011111
        n |= n >>> 1; n = 011111 | 001111 = 011111
        n |= n >>> 2;
        n |= n >>> 4;
        n |= n >>> 8;
        n |= n >>> 16;
        return (n < 0) ? 1 : (n >= MAXIMUM_CAPACITY) ? MAXIMUM_CAPACITY : n + 1; // return 32 100000
    }

    // 9 -> 1001
    static final int tableSizeFor(int cap) {
        n |= n >>> 1; // n = 1001 | 0100 = 1101
        n |= n >>> 2; // n = 1101 | 0011 = 1111
        n |= n >>> 4; // n = 1111 | 0000 = 1111
        n |= n >>> 8;
        n |= n >>> 16;
        return (n < 0) ? 1 : (n >= MAXIMUM_CAPACITY) ? MAXIMUM_CAPACITY : n + 1; // return 16 10000
    }

    // 32 -> 100000
    static final int tableSizeFor(int cap) {
        n |= n >>> 1; n = 100000 | 010000 = 110000
        n |= n >>> 2; n = 110000 | 001100 = 111100
        n |= n >>> 4; n = 111100 | 000011 = 111111
        n |= n >>> 8;
        n |= n >>> 16;
        return (n < 0) ? 1 : (n >= MAXIMUM_CAPACITY) ? MAXIMUM_CAPACITY : n + 1; // return 64 1000000
    }
```