"use strict";
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
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const path = __importStar(require("path"));
const multer_1 = __importDefault(require("multer"));
const promises_1 = __importDefault(require("fs/promises"));
const FRONTEND_STATIC_FOLDER_PATH = path.join(__dirname, "../../ur-frontend/dist");
//these should point to public directory of main election app
const CANDIDATE_DATA_JSON_PATH = path.join(__dirname, "../../../election-runner/public/candidate-data/");
const CANDIDATE_IMAGES_PATH = path.join(__dirname, "../../../election-runner/public/candidate-data/images");
console.log(CANDIDATE_IMAGES_PATH);
//multer config
const storage = multer_1.default.diskStorage({
    destination: (_, __, callback) => {
        callback(null, CANDIDATE_IMAGES_PATH);
    },
    filename: (_, file, callback) => {
        const ext = path.extname(file.originalname);
        const name = file.fieldname;
        callback(null, `${name}${ext}`);
    }
});
const uploadHandler = (0, multer_1.default)({ storage: storage });
const app = (0, express_1.default)();
const port = 3000;
app.use((req, _, next) => {
    console.log(`${req.url} got ${req.method}`);
    next();
});
app.use("/", express_1.default.static(FRONTEND_STATIC_FOLDER_PATH));
app.use("/", express_1.default.static(CANDIDATE_DATA_JSON_PATH));
app.use(express_1.default.json());
app.get("/", (_, response) => {
    response.redirect("/index.html");
});
app.get("/register", (_, response) => {
    response.redirect("/index.html");
});
app.post("/post/images", uploadHandler.any(), (request, response) => {
    var _a;
    // response.json({uploaded: request.files?.map((f:Multer.File) => f.filename)});
    response.json({ uploaded: ((_a = request.files) === null || _a === void 0 ? void 0 : _a.length) || -1 });
});
app.post("/post/posts-data", (request, response) => __awaiter(void 0, void 0, void 0, function* () {
    const data = request.body.postsData;
    const _fpath = path.join(CANDIDATE_DATA_JSON_PATH, request.body.candidateGroup + ".json");
    console.log(data);
    yield promises_1.default.writeFile(_fpath, JSON.stringify(data));
    response.json({ body: request.body });
}));
app.listen(port, () => {
    console.log(`Server running on port ${port}`);
    console.log("Access app at /index.html");
});
