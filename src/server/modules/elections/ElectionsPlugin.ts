import Elysia from "elysia";
import { CreateSessionBody, CreateSessionResponse } from "./types";
import { createSession } from "./ElectionsServices";
import { electionsDatabaseRepository } from "@/server/init";

const electionsPlugin = new Elysia({ prefix: "/elections" }).decorate("electionRepo", electionsDatabaseRepository).get(
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
);

export default electionsPlugin;
