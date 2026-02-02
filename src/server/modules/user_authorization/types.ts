import { t } from "elysia";

export const LoginBody = t.Object({
    identifier: t.String(),
    password: t.String(),
});

export type TLoginBody = typeof LoginBody.static

export type 