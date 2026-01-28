import Elysia, { t } from "elysia";
import { PostwiseCandidates, PostwiseCandidatesUpdation } from "./types";

import {
    registrationDatabaseRepository,
    registrationFileStorageRepository,
} from "@/server/init";

import { RegistrationService } from "./RegistrationService";

const registrationPlugin = new Elysia({
    prefix: "/register",
})
    .decorate("fileStorageRepo", registrationFileStorageRepository)
    .decorate("registrationRepo", registrationDatabaseRepository)
    .get(
        "/",
        async ({ registrationRepo }) => {
            return await RegistrationService.getAllPostwiseCandidates(
                registrationRepo,
            );
        },
        {
            response: t.Array(PostwiseCandidates),
        },
    )
    .post(
        "/",
        async ({ body, registrationRepo, fileStorageRepo }) => {
            await RegistrationService.updatePosts(
                body,
                registrationRepo,
                fileStorageRepo,
            );
            return { status: "success" };
        },
        {
            body: t.Array(PostwiseCandidatesUpdation),
        },
    );

export default registrationPlugin;
