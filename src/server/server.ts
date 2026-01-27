import Elysia from "elysia";

import { databaseProvider } from "./init";
import registrationPlugin from "@/server/modules/registration/RegistrationPlugin";

const databasePlugin = new Elysia()
    .onStart(async () => {
        await databaseProvider.connect();
    })
    .onStop(async () => {
        await databaseProvider.disconnect();
    });

const app = new Elysia({
    cookie: {
        secrets: "super-secret-string",
    },
    prefix: "/api",
})
    .use(databasePlugin)
    .use(registrationPlugin)
    .listen(5000);
export default app;
