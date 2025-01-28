import sqlite3 from 'sqlite3';

const db = new sqlite3.Database('./db/songs.db');

export default defineEventHandler(async (event) => {
  return new Promise((resolve, reject) => {
    db.all('SELECT * FROM songs', (err, rows) => {
      if (err) {
        reject(err);
      } else {
        resolve(rows);
      }
    });
  });
});