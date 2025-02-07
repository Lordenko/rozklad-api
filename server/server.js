import express from "express";
import cors from "cors";
import routes from "./routes.js";

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.static("public"));

app.use("/api", routes);

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`🚀 Сервер запущено на http://localhost:${PORT}`));


