import { createPortal } from 'react-dom';
import { Button } from './button';
import { cn } from '../../utils/helpers';

export const Modal = ({ isOpen, onClose, title, description, children, footer }) => {
  if (!isOpen) return null;

  return createPortal(
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/30 p-4">
      <div
        className={cn(
          'w-full max-w-lg rounded-2xl bg-white p-6 shadow-xl transition-transform',
        )}
      >
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-xl font-semibold text-text-primary">{title}</h3>
            {description && <p className="text-sm text-text-secondary">{description}</p>}
          </div>
          <Button variant="ghost" onClick={onClose}>
            ✕
          </Button>
        </div>
        <div className="mt-4 space-y-4 text-sm text-text-secondary">{children}</div>
        {footer && <div className="mt-6 flex justify-end gap-3">{footer}</div>}
      </div>
    </div>,
    document.body,
  );
};

