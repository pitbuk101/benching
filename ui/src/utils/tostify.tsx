import { toast, ToastOptions } from 'react-toastify';
import { BadgeCheck, CircleAlert, Info, TriangleAlert } from 'lucide-react';

interface IMessage {
  header?: string;
  subheader?: string;
  message?: string;
}

// Custom Toast content component
const ToastContent = ({ header, subheader, message }: IMessage) => (
  <div className="toast-content">
    <div className="toast-title">{header}</div>
    {subheader && <div className="toast-subtitle">{subheader}</div>}
    <div className="toast-message">{message}</div>
  </div>
);

class Toast {
  static id: number | string;

  // Success toast
  static success(msg?: IMessage, options?: ToastOptions<unknown>) {
    const {
      header = 'Success',
      subheader = '',
      message = 'Operation completed successfully',
    } = msg || {};

    this.id = toast.success(
      <ToastContent header={header} subheader={subheader} message={message} />,
      {
        autoClose: 3000,
        icon: <BadgeCheck className="stroke-green-500" />,
        className: 'toast-success',
        ...options,
      },
    );
    return () => Toast.dismiss(this.id);
  }

  // Error toast
  static error(msg?: IMessage, options?: ToastOptions<unknown>) {
    const {
      header = 'Error',
      subheader = '',
      message = 'An error occurred',
    } = msg || {};

    this.id = toast.error(
      <ToastContent header={header} subheader={subheader} message={message} />,
      {
        autoClose: 5000,
        icon: <CircleAlert className="stroke-red-500" />,
        className: 'toast-error',
        ...options,
      },
    );
    return () => Toast.dismiss(this.id);
  }

  // Warning toast
  static warning(msg?: IMessage, options?: ToastOptions<unknown>) {
    const {
      header = 'Warning',
      subheader = '',
      message = 'Please be cautious',
    } = msg || {};

    this.id = toast.warning(
      <ToastContent header={header} subheader={subheader} message={message} />,
      {
        autoClose: 4000,
        icon: <TriangleAlert className="stroke-yellow-500" />,
        className: 'toast-warning',
        ...options,
      },
    );
    return () => Toast.dismiss(this.id);
  }

  // Info toast
  static info(msg?: IMessage, options?: ToastOptions<unknown>) {
    const {
      header = 'Information',
      subheader = '',
      message = 'Here is some information',
    } = msg || {};

    this.id = toast.info(
      <ToastContent header={header} subheader={subheader} message={message} />,
      {
        autoClose: 3000,
        icon: <Info className="stroke-indigo-400" />,
        className: 'toast-info',
        ...options,
      },
    );
    return () => Toast.dismiss(this.id);
  }

  // Loading toast
  static loading(msg?: IMessage, options?: ToastOptions<unknown>) {
    const {
      header = 'Loading',
      subheader = '',
      message = 'Please wait...',
    } = msg || {};

    this.id = toast.loading(
      <ToastContent header={header} subheader={subheader} message={message} />,
      {
        autoClose: false,
        className: 'toast-loading',
        ...options,
      },
    );
    return () => Toast.dismiss(this.id);
  }

  // Update an existing toast
  static update(
    id: string | number,
    msg: IMessage,
    type: 'success' | 'error' | 'warning' | 'info',
    options?: ToastOptions<unknown>,
  ) {
    const { header = '', subheader = '', message = '' } = msg || {};

    toast.update(id, {
      render: (
        <ToastContent header={header} subheader={subheader} message={message} />
      ),
      type: type,
      ...options,
    });
  }

  // Dismiss a specific toast
  static dismiss(id?: string | number) {
    if (id) {
      toast.dismiss(id);
    }
  }

  // Dismiss all toasts
  static dismissAll() {
    toast.dismiss();
  }
}

export default Toast;
