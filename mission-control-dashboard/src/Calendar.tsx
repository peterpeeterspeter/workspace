import React from 'react';
import { useQuery } from './convex/_generated';

interface CalendarSummaryProps {
  onSelectSite?: (site: string) => void;
}

export const CalendarSummary: React.FC<CalendarSummaryProps> = ({ onSelectSite }) => {
  const summary = useQuery("calendar/getCalendarSummary", {});

  if (!summary) {
    return <div>Loading calendar summary...</div>;
  }

  const sites = Object.entries(summary.bySite).sort((a, b) => b[1] - a[1]);

  return (
    <div className="calendar-summary">
      <h2>📅 Content Calendar Summary</h2>

      <div className="summary-stats">
        <div className="stat-card">
          <h3>{summary.total}</h3>
          <p>Total Articles</p>
        </div>

        <div className="stat-card">
          <h3>{Object.keys(summary.bySite).length}</h3>
          <p>Sites</p>
        </div>

        <div className="stat-card">
          <h3>{summary.byPriority.high}</h3>
          <p>High Priority</p>
        </div>

        <div className="stat-card">
          <h3>{summary.byStatus.published || 0}</h3>
          <p>Published</p>
        </div>
      </div>

      <div className="sites-grid">
        <h3>By Site</h3>
        {sites.map(([site, count]) => (
          <div
            key={site}
            className="site-card"
            onClick={() => onSelectSite?.(site)}
            style={{ cursor: onSelectSite ? 'pointer' : 'default' }}
          >
            <h4>{site}</h4>
            <p>{count} articles</p>
          </div>
        ))}
      </div>

      <div className="status-breakdown">
        <h3>Status</h3>
        <div className="status-list">
          {Object.entries(summary.byStatus).map(([status, count]) => (
            <div key={status} className="status-item">
              <span className={`status-badge status-${status}`}>{status}</span>
              <span>{count}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

interface CalendarViewProps {
  site?: string;
  week?: number;
}

export const CalendarView: React.FC<CalendarViewProps> = ({ site, week }) => {
  const calendar = useQuery("calendar/getCalendar", { site, week }) ?? [];

  const groupedByWeek = calendar.reduce((acc, item) => {
    if (!acc[item.week]) {
      acc[item.week] = [];
    }
    acc[item.week].push(item);
    return acc;
  }, {} as Record<number, typeof calendar>);

  return (
    <div className="calendar-view">
      <h2>📅 Content Calendar</h2>
      {site && <p className="filter-text">Site: {site}</p>}
      {week && <p className="filter-text">Week: {week}</p>}

      {Object.entries(groupedByWeek)
        .sort(([a], [b]) => Number(a) - Number(b))
        .map(([weekNum, items]) => (
          <div key={weekNum} className="week-block">
            <h3>Week {weekNum}</h3>
            <div className="week-grid">
              {items.map((item) => (
                <div key={item._id} className="calendar-item">
                  <div className="item-header">
                    <span className={`priority priority-${item.priority}`}>
                      {item.priority}
                    </span>
                    <span className={`status-badge status-${item.status}`}>
                      {item.status}
                    </span>
                  </div>
                  <h4>{item.title}</h4>
                  <p className="site-name">{item.site}</p>
                  <p className="schedule-date">
                    {new Date(item.scheduledDate).toLocaleDateString()}
                  </p>
                  <div className="keywords">
                    {item.keywords.slice(0, 3).map((kw) => (
                      <span key={kw} className="keyword-tag">
                        {kw}
                      </span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
    </div>
  );
};
