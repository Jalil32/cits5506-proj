import { Toaster } from 'sonner';
import { AppSidebar } from './components/app-sidebar';
import { NotificationProvider } from './utils/NotificationContext';
import {
    Breadcrumb,
    BreadcrumbItem,
    BreadcrumbLink,
    BreadcrumbList,
    BreadcrumbPage,
    BreadcrumbSeparator,
} from '@/components/ui/breadcrumb';
import { Separator } from '@/components/ui/separator';
import {
    SidebarInset,
    SidebarProvider,
    SidebarTrigger,
} from '@/components/ui/sidebar';
import { ThemeProvider } from './components/theme-provider';
import {
    BrowserRouter,
    Routes,
    Route,
    Navigate,
    useLocation,
} from 'react-router-dom';
import './App.css';
import HomePage from './pages/home';
import LiveStreamPage from './pages/LiveStream';

// Content Layout Component with dynamic breadcrumb
function ContentLayout() {
    const location = useLocation();
    const path = location.pathname;

    // Determine current page title based on path
    const getCurrentPage = () => {
        if (path === '/home') return 'Home';
        if (path === '/livestream') return 'LiveStream';
        return 'Dashboard';
    };

    return (
        <SidebarInset className="flex flex-col w-full">
            <header className="flex h-16 shrink-0 items-center gap-2 border-b px-4">
                <SidebarTrigger className="-ml-1" />
                <Separator orientation="vertical" className="mr-2 h-4" />
                <Breadcrumb>
                    <BreadcrumbList>
                        <BreadcrumbItem className="hidden md:block">
                            <BreadcrumbLink href="#">Dashboard</BreadcrumbLink>
                        </BreadcrumbItem>
                        <BreadcrumbSeparator className="hidden md:block" />
                        <BreadcrumbItem>
                            <BreadcrumbPage>{getCurrentPage()}</BreadcrumbPage>
                        </BreadcrumbItem>
                    </BreadcrumbList>
                </Breadcrumb>
            </header>
            <div className="flex-1 overflow-hidden px-4 py-4">
                <Routes>
                    <Route path="/home" element={<HomePage />} />
                    <Route path="/livestream" element={<LiveStreamPage />} />
                    <Route path="/" element={<Navigate to="/home" replace />} />
                </Routes>
            </div>
        </SidebarInset>
    );
}

export default function App() {
    return (
		<NotificationProvider>
			<BrowserRouter>
				<ThemeProvider defaultTheme="light" storageKey="vite-ui-theme">
					<SidebarProvider>
						<div className="flex h-screen w-screen overflow-hidden bg-zinc-950">
						<AppSidebar className="h-full" />
						<ContentLayout />
						</div>
					</SidebarProvider>
				</ThemeProvider>
				<Toaster/>
			</BrowserRouter>
		</NotificationProvider>
    );
}
