import type { TUUID } from "@/server/modules/common/types";

export interface IDatabaseRepository {
    fetchPasswordHash(user_id: TUUID): Promise<string | null>;
    getUserId(identifier: string): Promise<TUUID | null>
    createNewUser(user_id: TUUID, identifier: string, password_hash: string): Promise<void>;
}
