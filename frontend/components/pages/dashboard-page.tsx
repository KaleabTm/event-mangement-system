"use client";

import { Button } from "@/components/ui/button";
import { Tabs, TabsContent } from "@/components/ui/tabs";
import { DASHBOARD_PAGE } from "@/constants/colors";
import { Plus } from "lucide-react";
import { useState } from "react";
import EventModal from "../modals/event-modal";
import CalendarView from "../modules/calendar-view";
import ListView from "../modules/list-view";
import DashboardLayout from "../shared/layout/dashboard-layout";
import CalendarSidebar from "../shared/navigations/calendar-sidebar";
import DashboardTabs from "../shared/navigations/dashboard-tabs";

export default function DashboardPage() {
	const [isEventModalOpen, setIsEventModalOpen] = useState(false);
	const [editingEvent, setEditingEvent] = useState(null);

	const handleCreateEvent = () => {
		setEditingEvent(null);
		setIsEventModalOpen(true);
	};

	const handleEditEvent = (event: any) => {
		setEditingEvent(event);
		setIsEventModalOpen(true);
	};

	return (
		<DashboardLayout>
			<div className="flex gap-6">
				{/* Calendar Sidebar */}
				<CalendarSidebar />

				{/* Main Content Area */}
				<div className="flex-1 space-y-6">
					<div className="flex justify-between items-center">
						<h2 className="text-3xl font-bold tracking-tight">
							{DASHBOARD_PAGE.SECTIONS.HEADER}
						</h2>
						<Button onClick={handleCreateEvent} className="flex items-center">
							<Plus className="h-4 w-4 mr-2" />
							Create Event
						</Button>
					</div>

					<Tabs defaultValue="calendar">
						<DashboardTabs />
						<TabsContent value="calendar" className="space-y-4">
							<CalendarView onEditEvent={handleEditEvent} />
						</TabsContent>

						<TabsContent value="list" className="space-y-4">
							<ListView onEditEvent={handleEditEvent} />
						</TabsContent>
					</Tabs>
				</div>
			</div>

			{/* Event Modal */}
			<EventModal
				isOpen={isEventModalOpen}
				onClose={() => setIsEventModalOpen(false)}
				event={editingEvent}
			/>
		</DashboardLayout>
	);
}
