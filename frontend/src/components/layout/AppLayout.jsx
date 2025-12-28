import { Sidebar } from './Sidebar';
import { Header } from './Header';
import { Footer } from './Footer';

/**
 * Provides the shell used across protected pages: sidebar + header + main area.
 */
export const AppLayout = ({ children }) => (
  <div className="min-h-screen bg-background-secondary text-text-primary">
    <div className="flex">
      <Sidebar />
      <div className="flex min-h-screen flex-1 flex-col">
        <Header />
        <main className="flex-1 px-4 py-6 md:px-8 lg:px-10">{children}</main>
        <Footer />
      </div>
    </div>
  </div>
);

