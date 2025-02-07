import express from "express";
import fs from "fs";
import { exec } from "child_process";

const router = express.Router();
const dataFilePath = "./api/rozklad.json";

// Запускає Python
router.get("/run_parser",(req, res) => {
    const { group } = req.query;
});

// Отримаємо данні
router.get("/data",(req, res) => {
    if(!fs.existsSync(dataFilePath)) {
        return res.status(404).json({ error: "Файл не знайдено" })
    }
    try {
        const rawData = fs.readFileSync(dataFilePath, "utf-8");
        const data = rawData ? JSON.parse(rawData) : {};
        res.json(data);
    } catch (error) {
        console.error("Помилка читання JSON:", error);
        res.status(500).json({ error: "Помилка парсингу JSON" });
    }
});

export default router;

