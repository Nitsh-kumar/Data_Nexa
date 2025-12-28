import { NavLink } from 'react-router-dom';
import { routes } from '../../config/routes';

const menu = [
  { label: 'Dashboard', to: routes.DASHBOARD },
  { label: 'Upload', to: routes.UPLOAD },
  { label: 'Analysis', to: routes.ACTION_CENTER.replace(':id', 'latest') },
  { label: 'Settings', to: routes.SETTINGS_PROFILE },
];

export const Sidebar = () => (
  <aside className="hidden w-64 flex-shrink-0 border-r border-gray-200 bg-white px-4 py-6 lg:block">
    <h2 className="mb-6 text-xl font-semibold text-primary-600">DataInsight Pro</h2>
    <nav className="space-y-2">
      {menu.map((item) => (
        <NavLink
          key={item.to}
          to={item.to}
          className={({ isActive }) =>
            [
              'block rounded-lg px-3 py-2 text-sm font-medium transition-colors',
              isActive ? 'bg-primary-50 text-primary-700' : 'text-text-secondary hover:bg-gray-50',
            ].join(' ')
          }
        >
          {item.label}
        </NavLink>
      ))}
    </nav>
  </aside>
);

