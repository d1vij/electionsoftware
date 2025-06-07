import express from "express";
import * as path from "path";
import multer from "multer";
import fs from "fs/promises";


const FRONTEND_STATIC_FOLDER_PATH = path.join(__dirname, "..", "..", "ur-frontend", "dist");
const CANDIDATE_DATA_JSON_PATH = path.join(__dirname, "../../ur-frontend/CANDIDATE_DATA/candidates.json");
const CANDIDATE_IMAGES_PATH = path.join(__dirname, "../../ur-frontend/CANDIDATE_DATA/images");

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
const port = 5000;


app.use((req, _, next) => {
    console.log(`${req.url} got ${req.method}`);
    next();
})
app.use("/", express.static(FRONTEND_STATIC_FOLDER_PATH));
app.use("/", express.static(CANDIDATE_DATA_JSON_PATH));
app.use(express.json());


app.post("/post/images", uploadHandler.any(), (request, response) => {
    // response.json({uploaded: request.files?.map((f:Multer.File) => f.filename)});
    response.json({uploaded: request.files?.length || -1});
})
app.post("/post/posts-data",async (request, response)=>{
    const data = request.body;
    console.log(data);
    await fs.writeFile(CANDIDATE_DATA_JSON_PATH, JSON.stringify(data));
    response.json({body:data});
})

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
    console.log("Access app at /index.html");
})