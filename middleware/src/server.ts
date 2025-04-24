import express, { type Request, type Response } from "express";

// Initialize express app
const app = express();
const port = process.env.PORT || 3000;

// Middleware for parsing JSON bodies
app.use(express.json());
// Middleware for parsing URL-encoded bodies
app.use(express.urlencoded({ extended: true }));

// Define a simple route
app.get("/", (_: Request, res: Response) => {
	res.send("Hello World from Express with TypeScript!");
});

// Start the server
app.listen(port, () => {
	console.log(`Server running at http://localhost:${port}`);
});
