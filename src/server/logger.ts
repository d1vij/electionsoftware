import chalk from "chalk";
import Elysia from "elysia";

const marker = `[${chalk.green("*")}]`;

const loggerPlugin = new Elysia().onRequest(({ request }) => {
    console.log(`${marker} ${chalk.yellow(request.method)} on ${request.url}`);
});

export default loggerPlugin;
