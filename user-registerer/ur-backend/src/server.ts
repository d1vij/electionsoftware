/**
 * Server for user registerer

 * static files in /user-registerer/ur-frontend/dist/
 * saves images & candidate data in /election-runner/public/candidate-data/
 *
 * -> To register candidates, simply node run this file and go to /index.html
 * NOTE: Existing Candidates data is not re-loaded again, which means even for a single edit,
 *       all the candidates have to be registered, or otherwise candidate data can be edited manually
 *       ensuring that each candidate has a unique uuid (candidateId) and its corresponding image in /image/ folder
 *
 * -> Image of candidates are saved with candidates uuid as filename and as .png extension irrespective of source extension
 **/


import express, { Request, Response,NextFunction } from "express";
import * as path from "path";
import multer from "multer";
import fs from "fs/promises";
import chalk from "chalk";


const FRONTEND_STATIC_FOLDER_PATH = path.join(__dirname, "../../ur-frontend/dist");

//these should point to public directory of main election app
const CANDIDATE_DATA_JSON_PATH = path.join(__dirname, "../../../election-runner/public/candidate-data/");
const CANDIDATE_IMAGES_PATH = path.join(__dirname, "../../../election-runner/public/candidate-data/images");
console.log(CANDIDATE_IMAGES_PATH)

//multer config
const storage = multer.diskStorage({
    destination: (_, __, callback) => {
        callback(null, CANDIDATE_IMAGES_PATH);
    },
    filename: (_, file, callback) => {
        const ext = path.extname(file.originalname);
        const name = file.fieldname
        callback(null, `${name}${ext}`);
    }
})
const uploadHandler = multer({storage: storage})

const app = express();
const port = 3000;

app.use(logger)
app.use("/", express.static(FRONTEND_STATIC_FOLDER_PATH));
app.use("/", express.static(CANDIDATE_DATA_JSON_PATH));
app.use(express.json());

app.get("/",(_, response)=>{
    response.redirect("/index.html")
})
app.get("/register",(_, response)=>{
    response.redirect("/index.html")
})


app.post("/post/images", uploadHandler.any(), (request, response) => {
    // response.json({uploaded: request.files?.map((f:Multer.File) => f.filename)});
    response.json({uploaded: request.files?.length || -1});
})
app.post("/post/posts-data",async (request, response)=>{
    const data = request.body.postsData;
    const _fpath = path.join(CANDIDATE_DATA_JSON_PATH, request.body.candidateGroup + ".json")
    console.log(data);
    await fs.writeFile(_fpath, JSON.stringify(data));
    response.json({body:request.body})
})

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
    console.log("Access app at /index.html");
})

async function logger(request:Request, response:Response, next:NextFunction){
    switch(request.method){
        case("GET"):{
            console.log(`${chalk.yellow("USER-REGISTERER")} ${chalk.green("GET")} on ${request.url} `)
            break;
        }
        case("GET"):{
            console.log(`${chalk.yellow("USER-REGISTERER")} ${chalk.blue("POST")} on ${request.url} `)
            break;
        }
        case("GET"):{
            console.log(`${chalk.yellow("USER-REGISTERER")} ${chalk.red("DELETE")} on ${request.url} `)
            break;
        }
        default:{
            console.log(`${chalk.yellow("USER-REGISTERER")} ${chalk.grey(request.method)} on ${request.url} `)
            break;
        }
    }

    next();
}
