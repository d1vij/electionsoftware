import Elysia from "elysia";

import { databaseProvider } from "@/server/init";
import registrationPlugin from "@/server/modules/registration/RegistrationPlugin";
import loggerPlugin from "@/server/logger";
import electionsPlugin from "./modules/elections/ElectionsPlugin";

const PORT = 5000;

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
    .use(loggerPlugin)
    .use(databasePlugin)
    // routes
    .use(registrationPlugin)
    .use(electionsPlugin)
    .listen(PORT);
export default app;

console.log(`Server listening on ${PORT}`);
