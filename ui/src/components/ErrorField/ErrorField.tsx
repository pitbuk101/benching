import { CircleX } from 'lucide-react';

const ErrorField = ({ msg }: { msg?: string }) => {
  if (!msg) return null;
  return (
    <div className="error-text">
      <CircleX className="error-icon" size={15} />
      <p>{msg}</p>
    </div>
  );
};

export default ErrorField;
