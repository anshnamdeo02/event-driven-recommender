const API_KEY = "c5f098b11f9786b753d7521cdc1dd430";

export async function getPoster(title: string) {
  try {
    const r = await fetch(
      `https://api.themoviedb.org/3/search/movie?api_key=${API_KEY}&query=${encodeURIComponent(title)}`
    );

    const data = await r.json();

    if (!data.results || data.results.length === 0)
      return null;

    return `https://image.tmdb.org/t/p/w500${data.results[0].poster_path}`;
  } catch {
    return null;
  }
}
