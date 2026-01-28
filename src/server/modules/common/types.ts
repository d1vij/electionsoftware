import { t } from "elysia";

export const UUID = t.String({
    format: "uuid",
});

export type TUUID = typeof UUID.static;
