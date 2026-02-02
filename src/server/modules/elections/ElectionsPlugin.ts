import Elysia from "elysia";
import { CreateSessionBody, CreateSessionResponse } from "./types";
import { createSession } from "./ElectionsServices";
import { electionsDatabaseRepository } from "@/server/init";

const electionsPlugin = new Elysia({ prefix: "/elections" })
    .decorate("electionRepo", electionsDatabaseRepository)
    // Authorized user requests for vote session
    .get(
        "/session",
        async ({ body, electionRepo }) => {
            const session_id = await createSession(electionRepo, body.invoker_id);

            return {
                session_id: session_id,
            };
        },
        {
            body: CreateSessionBody,
            response: CreateSessionResponse,
        },
    )
    // Vote submission endpoint
    .post("/submit", async () => { }, {
        
    });

export default electionsPlugin;
