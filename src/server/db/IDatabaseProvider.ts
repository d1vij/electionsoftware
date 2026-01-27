import type { VoidPromise } from "../types";

export interface IDatabaseProvider<T> {
    connect(): VoidPromise;
    disconnect(): VoidPromise;
    ping(): VoidPromise;
    getInstance(): T;
}
