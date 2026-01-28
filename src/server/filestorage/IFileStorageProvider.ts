import type { BunFile } from "bun";
import type { TImageFile } from "./types";

export interface IFileStorageProvider {
    saveFile(file: TImageFile, id: string): Promise<void>;
    deleteFile(id: string): Promise<void>;
    getFile(id: string): Promise<BunFile>;
}
