import Elysia, { t } from "elysia";
import { LoginBody } from "./types";

import { userAuthorizationDatabaseRepository } from "@/server/init";

const userAuthPlugin = new Elysia({
    prefix: "/auth",
    cookie: {
        
    }
})

    .decorate("userAuthDatabaseRepo", userAuthorizationDatabaseRepository)
    .get("/logout", () => {
        
    }, {
        cookie:
    } )
    .post(
        "/login",
        async ({ userAuthDatabaseRepo, body, status, cookie: { auth_id } }) => {
            const { identifier, password } = body;

            const password_hash = await userAuthDatabaseRepo.fetchPasswordHash(identifier);
            if (password_hash === null) {
                return status("Not Found", "no user found with provided identifier");
            }

            if ((await Bun.password.verify(password, password_hash)) === false) {
                return status("Unauthorized", "incorrect password");
            }

            const userId = await userAuthDatabaseRepo.getUserId(identifier);
            if (userId === null) {
                return status("Internal Server Error", "no uuid found for provided identifier");
            }

            auth_id.value = userId;
            auth_id.maxAge = 3600; // expire after a day

            return {
                status: "success",
            };
        },
        {
            body: LoginBody,
            cookie: t.Object({
                auth_id: t.Optional(t.String()),
            }),
        },
    );
