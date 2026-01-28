import type { TUUID } from "@/server/modules/common/types";
import type { IDatabaseRepository } from "./repositories/IDatabaseRepository";

export async function createSession(electionRepo: IDatabaseRepository, invoker_id: TUUID): Promise<TUUID> {
    const session_id = Bun.randomUUIDv7();
    await electionRepo.insertVoteSessionUUID(invoker_id, session_id);
    return session_id;
}
