
export function formatDate(date) {
    const yyyy = date.getFullYear();
    const mm = String(date.getMonth() + 1).padStart(2, '0'); // Months are zero-based
    const dd = String(date.getDate()).padStart(2, '0');
    const hh = String(date.getHours()).padStart(2, '0');
    const min = String(date.getMinutes()).padStart(2, '0');
    const ss = String(date.getSeconds()).padStart(2, '0');
  
    return `${yyyy}/${mm}/${dd} ${hh}:${min}:${ss}`;
  }

export  const syslog_priority_colors = [
            '#ff0000', // red
            '#800080', // purple
            '#ffa500', // orange
            '#008000', // green
            '#add8e6', // light blue
        ];
export const syslog_priority_labels = [
            'Error',
            'Critical',
            'Warning',
            'Notice',
            'Info']

