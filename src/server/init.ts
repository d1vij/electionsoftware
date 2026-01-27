import path from "path";
import { SqliteProvider } from "@/server/db/providers";

import { SqliteRegistrationRepository } from "@/server/modules/registration/repositories";
import { RegistrationService } from "./modules/registration/RegistrationService";
import type { IDatabaseProvider } from "@/server/db";

// PROVIDERS
export const sqliteProvider = new SqliteProvider(
    path.join(import.meta.dir, "..", "..", "data/app.db"),
);
const DATABASE_TYPE = "sqlite";

// REPOSITORIES
export const registrationRepository =
    DATABASE_TYPE == "sqlite"
        ? new SqliteRegistrationRepository(sqliteProvider.getInstance())
        : new SqliteRegistrationRepository(sqliteProvider.getInstance());

// SERVICES
export const registrationService = new RegistrationService(
    registrationRepository,
);

// DATABASE
export const databaseProvider: IDatabaseProvider<unknown> =
    DATABASE_TYPE == "sqlite" ? sqliteProvider : sqliteProvider;
