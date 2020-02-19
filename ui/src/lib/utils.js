export function convertDate(date) {
  const dateObj = new Date(date);
  const hours = `${dateObj.getHours() < 10 ? '0' : ''}${dateObj.getHours()}`;
  const minutes = `${dateObj.getMinutes() < 10 ? '0' : ''}${dateObj.getMinutes()}`;
  const month = `${dateObj.getMonth() + 1 < 10 ? '0' : ''}${dateObj.getMonth() + 1}`;
  const day = `${dateObj.getDate() < 10 ? '0' : ''}${dateObj.getDate()}`;
  return `${day}-${month}-${dateObj.getFullYear()} ${hours}:${minutes}`;
}
