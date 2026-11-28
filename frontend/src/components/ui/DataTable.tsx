'use client';

import React from 'react';

export interface DataColumn<T> {
  key: string;
  header: string;
  align?: 'left' | 'right';
  render: (row: T) => React.ReactNode;
  className?: string;
}

export function DataTable<T>({
  data,
  columns,
  rowKey,
  onRowClick,
  emptyState,
  dense = false,
  ariaLabel = 'Data table',
}: {
  data: T[];
  columns: DataColumn<T>[];
  rowKey: (row: T) => string;
  onRowClick?: (row: T) => void;
  emptyState?: React.ReactNode;
  dense?: boolean;
  ariaLabel?: string;
}) {
  if (data.length === 0 && emptyState) {
    return <>{emptyState}</>;
  }

  const cellPad = dense ? 'px-3 py-2' : 'px-4 py-3';

  return (
    <div className="rounded-xl border border-line bg-panel overflow-hidden">
      <div className="overflow-x-auto">
        <table role="table" aria-label={ariaLabel} className="w-full border-collapse text-left">
          <thead>
            <tr role="row" className="border-b border-line bg-surface">
              {columns.map((col) => (
                <th
                  key={col.key}
                  scope="col"
                  className={`${cellPad} text-xs font-semibold text-muted ${
                    col.align === 'right' ? 'text-right' : 'text-left'
                  } ${col.className || ''}`}
                >
                  {col.header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-line-subtle">
            {data.map((row) => (
              <tr
                key={rowKey(row)}
                role="row"
                onClick={onRowClick ? () => onRowClick(row) : undefined}
                className={`transition-colors ${
                  onRowClick ? 'hover:bg-surface-hover cursor-pointer' : 'hover:bg-surface/50'
                }`}
              >
                {columns.map((col) => (
                  <td
                    key={col.key}
                    className={`${cellPad} text-sm text-fg ${
                      col.align === 'right' ? 'text-right tabular-aml' : ''
                    } ${col.className || ''}`}
                  >
                    {col.render(row)}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
