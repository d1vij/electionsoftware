import type { TImageFile } from "@/server/filestorage/types";

export interface IFileStorageRepository {
    saveCandidateImage(image: TImageFile, id: string): Promise<void>;
    deleteCandidateImage(id: string): Promise<void>;
}
