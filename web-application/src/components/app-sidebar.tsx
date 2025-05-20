import * as React from 'react';
import {
    AudioWaveform,
    Command,
    GalleryVerticalEnd,
    Home,
    VideoIcon,
} from 'lucide-react';

import { NavProjects } from '@/components/nav-projects';
import { TeamSwitcher } from '@/components/team-switcher';
import {
    Sidebar,
    SidebarContent,
    SidebarHeader,
} from '@/components/ui/sidebar';

// This is sample data.
const data = {
    teams: [
        {
            name: 'Smart Security Inc',
            logo: GalleryVerticalEnd,
            plan: 'CITS5506',
        },
    ],
    projects: [
        {
            name: 'Home',
            url: '/home',
            icon: Home,
        },
        {
            name: 'LiveStream',
            url: '/livestream',
            icon: VideoIcon,
        },
    ],
};

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
    return (
        <Sidebar collapsible="icon" {...props}>
            <SidebarHeader>
                <TeamSwitcher teams={data.teams} />
            </SidebarHeader>
            <SidebarContent>
                <NavProjects projects={data.projects} />
            </SidebarContent>
        </Sidebar>
    );
}
