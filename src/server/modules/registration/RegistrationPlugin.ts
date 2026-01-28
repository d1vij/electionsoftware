import Elysia, { t } from "elysia";
import { CandidateImageUpload, PostwiseCandidates, PostwiseCandidatesUpdation } from "./types";

import { registrationDatabaseRepository, registrationFileStorageRepository } from "@/server/init";

import { getAllPostwiseCandidates, updatePosts, uploadCandidateImages } from "./RegistrationServices";

const registrationPlugin = new Elysia({
    prefix: "/register",
})
    .decorate("fileStorageRepo", registrationFileStorageRepository)
    .decorate("registrationRepo", registrationDatabaseRepository)
    .get(
        "/",
        async ({ registrationRepo }) => {
            return await getAllPostwiseCandidates(registrationRepo);
        },
        {
            response: t.Array(PostwiseCandidates),
        },
    )
    .post(
        "/upload/images",
        async ({ fileStorageRepo, body }) => {
            await uploadCandidateImages(fileStorageRepo, body);
        },
        {
            body: CandidateImageUpload,
        },
    )
    .post(
        "/upload/data",
        async ({ body, registrationRepo }) => {
            await updatePosts(body, registrationRepo);
            return { status: "success" };
        },
        {
            body: t.Array(PostwiseCandidatesUpdation),
        },
    );

export default registrationPlugin;
