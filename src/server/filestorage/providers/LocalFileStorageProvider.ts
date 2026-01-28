import type { BunFile } from "bun";
import type { IFileStorageProvider } from "../IFileStorageProvider";
import type { TImageFile } from "../types";

export class LocalFileStorageProvider implements IFileStorageProvider {
    private directory: string;
    constructor(directory: string) {
        this.directory = directory;
    }

    /**
     * Creates a new image, or overwrites existing one with same id
     */
    public async saveFile(image: TImageFile, id: string): Promise<void> {
        const file = Bun.file(`${this.directory}/${id}`);
        await Bun.write(file, image);
    }

    public async getFile(id: string): Promise<BunFile> {
        const file = Bun.file(`${this.directory}/${id}`);
        if ((await file.exists()) === false) {
            throw new Error(`no file exists with id ${id}`);
        }
        return file;
    }

    public async deleteFile(id: string): Promise<void> {
        const file = Bun.file(`${this.directory}/${id}`);
        if (!(await file.exists())) {
            throw new Error(`no file exists with id ${id}`);
        }
        await file.delete();
    }
}
