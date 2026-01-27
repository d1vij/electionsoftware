import Elysia, { t } from "elysia";
import { PostwiseCandidates, PostwiseCandidatesUpdation } from "./types";

import { registrationRepository } from "@/server/init";

const registrationPlugin = new Elysia({
    prefix: "/register",
})
    .get(
        "/",
        async () => {
            const results =
                await registrationRepository.getAllCandidatesPostwise();
            return results;
        },
        {
            response: t.Array(PostwiseCandidates),
        },
    )
    .post("/", async () => {}, {
        parse: "json",
        body: t.Array(PostwiseCandidatesUpdation),
    });

export default registrationPlugin;
