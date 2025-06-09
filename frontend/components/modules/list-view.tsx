"use client";

import { useCalendars } from "@/actions/query/calendars";
import { useDeleteEvent, useEvents } from "@/actions/query/events";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useCalendarVisibility } from "@/hooks/use-calendar-visibility";
import { exportSingleEvent } from "@/lib/ics-export";
import { Calendar, Clock, Download, Edit, Repeat, Trash2 } from "lucide-react";
import EmptyState from "../shared/ui/empty-state";
import LoadingSpinner from "../shared/ui/loading-spinner";

interface ListViewProps {
	onEditEvent: (event: any) => void;
}

export default function ListView({ onEditEvent }: ListViewProps) {
	const { data: events = [], isLoading: eventsLoading } = useEvents();
	const { data: calendars = [], isLoading: calendarsLoading } = useCalendars();
	const { visibleCalendarIds } = useCalendarVisibility();
	const deleteEventMutation = useDeleteEvent();

	const isLoading =
		eventsLoading || calendarsLoading || deleteEventMutation.isPending;

	// Filter visible events
	const visibleEvents = events.filter((event) =>
		visibleCalendarIds.includes(event.calendar.id)
	);

	// Sort events by start_time date
	const sortedEvents = [...visibleEvents].sort(
		(a, b) => new Date(a.start_time).getTime() - new Date(b.start_time).getTime()
	);

	// Filter upcoming events
	const upcomingEvents = sortedEvents
		.filter((event) => new Date(event.start_time) >= new Date())
		.slice(0, 20);

	const formatDate = (dateString: string) => {
		const date = new Date(dateString);
		return date.toLocaleDateString("en-US", {
			weekday: "short",
			year: "numeric",
			month: "short",
			day: "numeric",
		});
	};

	const formatTime = (dateString: string) => {
		const date = new Date(dateString);
		return date.toLocaleTimeString("en-US", {
			hour: "numeric",
			minute: "2-digit",
			hour12: true,
		});
	};

	const getRecurrenceText = (recurrence: any) => {
		switch (recurrence.frequency) {
			case "daily":
				return recurrence.interval === 1
					? "Daily"
					: `Every ${recurrence.interval} days`;
			case "weekly":
				return recurrence.interval === 1
					? "Weekly"
					: `Every ${recurrence.interval} weeks`;
			case "monthly":
				return recurrence.interval === 1
					? "Monthly"
					: `Every ${recurrence.interval} months`;
			case "yearly":
				return "Yearly";
			case "custom":
				return "Custom";
			default:
				return null;
		}
	};

	const handleDelete = async (eventId: string) => {
		if (confirm("Are you sure you want to delete this event?")) {
			deleteEventMutation.mutate(eventId);
		}
	};

	if (isLoading) {
		return (
			<Card>
				<CardContent className="py-12">
					<LoadingSpinner text="Loading events..." />
				</CardContent>
			</Card>
		);
	}

	if (upcomingEvents.length === 0) {
		return (
			<Card>
				<CardContent>
					<EmptyState
						icon={Calendar}
						title="No upcoming events"
						description="Create your first event to get started with managing your schedule."
					/>
				</CardContent>
			</Card>
		);
	}

	return (
		<div className="space-y-4">
			<Card>
				<CardHeader>
					<CardTitle className="flex items-center">
						<Calendar className="h-5 w-5 mr-2" />
						Upcoming Events ({upcomingEvents.length})
					</CardTitle>
				</CardHeader>
				<CardContent className="space-y-4">
					{upcomingEvents.map((event) => (
						<div
							key={event.id}
							className="flex items-start justify-between p-4 border rounded-lg hover:bg-gray-50 transition-colors"
						>
							<div className="flex-1">
								<div className="flex items-start justify-between mb-2">
									<div className="flex items-center space-x-2">
										<h3 className="font-medium text-gray-900">{event.title}</h3>
										{(() => {
											const calendar = calendars.find((c) => c.id === event.calendar.id);
											return calendar ? (
												<Badge
													variant="outline"
													className="text-xs flex items-center space-x-1"
												>
													<div
														className="w-2 h-2 rounded-full"
														style={{ backgroundColor: calendar.color }}
													/>
													<span>{calendar.name}</span>
												</Badge>
											) : null;
										})()}
									</div>
									<div
										className="w-3 h-3 rounded-full ml-2 mt-1"
										style={{ backgroundColor: event.color ?? undefined }}
									/>
								</div>

								{event.description && (
									<p className="text-sm text-gray-600 mb-2">{event.description}</p>
								)}

								<div className="flex items-center space-x-4 text-sm text-gray-500">
									<div className="flex items-center">
										<Calendar className="h-4 w-4 mr-1" />
										{formatDate(event.start_time)}
									</div>
									{!event.is_all_day && (
										<div className="flex items-center">
											<Clock className="h-4 w-4 mr-1" />
											{formatTime(event.start_time)} - {formatTime(event.end_time)}
										</div>
									)}
									{event.recurrence.frequency !== "none" && (
										<div className="flex items-center">
											<Repeat className="h-4 w-4 mr-1" />
											<Badge variant="secondary" className="text-xs">
												{getRecurrenceText(event.recurrence)}
											</Badge>
										</div>
									)}
								</div>
							</div>

							<div className="flex items-center space-x-2 ml-4">
								<Button
									variant="outline"
									size="sm"
									onClick={() => exportSingleEvent(event)}
									title="Export event"
								>
									<Download className="h-4 w-4" />
								</Button>
								<Button variant="outline" size="sm" onClick={() => onEditEvent(event)}>
									<Edit className="h-4 w-4" />
								</Button>
								<Button
									variant="outline"
									size="sm"
									onClick={() => handleDelete(event.id)}
									disabled={deleteEventMutation.isPending}
								>
									<Trash2 className="h-4 w-4" />
								</Button>
							</div>
						</div>
					))}
				</CardContent>
			</Card>
		</div>
	);
}
