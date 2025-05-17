import express from 'express';
import videoRoutes from './routes/videoRoutes';
import cors from 'cors';

// 1) Initialize express app
const app = express();
const port = process.env.PORT || 3000;

// 2 Setup CORS
app.use(
    cors({
        // During development, allow requests from React's dev server
        origin:
            process.env.NODE_ENV === 'production'
                ? process.env.FRONTEND_URL
                : 'http://localhost:5173',
        methods: ['GET', 'POST'],
        credentials: true,
    }),
);

// 2) Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(videoRoutes);

// 3) Start the server
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
