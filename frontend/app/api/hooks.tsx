import useSWR from 'swr';

const fetcher = (...args) => fetch(...args).then((res) => res.json());

export function useFolders() {
    const { data, error, isLoading } = useSWR('http://localhost:8000/api/folders', fetcher, {revalidateOnFocus: false});

    return {
        folders: data,
        isLoading,
        isError: error
    }
}