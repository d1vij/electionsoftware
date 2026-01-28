import type { TImageFile } from "@/server/filestorage/types";
import type { IFileStorageRepository } from "./IFileStorageRepository";
import type { LocalFileStorageProvider } from "@/server/filestorage/providers/LocalFileStorageProvider";

export class LocalFileStorageRepository implements IFileStorageRepository {
    private fs;
    public constructor(fs: LocalFileStorageProvider) {
        this.fs = fs;
    }
    public async saveCandidateImage(
        image: TImageFile,
        id: string,
    ): Promise<void> {
        await this.fs.saveFile(image, id);
    }

    public async deleteCandidateImage(id: string): Promise<void> {
        await this.fs.deleteFile(id);
    }
}
