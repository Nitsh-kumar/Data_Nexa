/**
 * DataPreview uses a render prop so consumers can either use the default table
 * or inject a custom view (for instance react-window or a virtualized grid).
 */
export const DataPreview = ({ data = { columns: [], rows: [] }, render }) => {
  if (render) {
    return render(data);
  }

  return (
    <div className="overflow-hidden rounded-2xl border border-gray-100 bg-white">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-100 text-sm">
          <thead className="bg-background-tertiary">
            <tr>
              {data.columns.map((column) => (
                <th
                  key={column}
                  className="px-4 py-3 text-left text-xs font-medium uppercase tracking-wider text-text-tertiary"
                >
                  {column}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-50 bg-white">
            {data.rows.map((row, rowIndex) => (
              <tr key={rowIndex} className="hover:bg-background-secondary">
                {data.columns.map((column) => (
                  <td key={column} className="whitespace-nowrap px-4 py-3 text-text-secondary">
                    {row[column]}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p className="border-t border-gray-100 px-4 py-2 text-xs text-text-tertiary">
        Showing {data.rows.length} sample rows · {data.columns.length} columns
      </p>
    </div>
  );
};

