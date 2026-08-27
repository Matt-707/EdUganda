from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import os
import time


# ============================================================
# 1. LOAD THE EMBEDDING MODEL ONCE
# ============================================================

print("🧠 Loading embedding model...")

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

print("✅ Embedding model loaded.")


# ============================================================
# 2. CHECK WHETHER A DIRECTORY CONTAINS A VALID FAISS INDEX
# ============================================================

def is_valid_faiss_index(path):
    """
    Check whether the given directory contains the two files
    required for a LangChain FAISS index.

    A valid saved FAISS index normally contains:

        index.faiss
        index.pkl
    """

    faiss_file = os.path.join(path, "index.faiss")
    pickle_file = os.path.join(path, "index.pkl")

    return (
        os.path.isfile(faiss_file)
        and
        os.path.isfile(pickle_file)
    )


# ============================================================
# 3. FIND ALL FAISS INDEXES
# ============================================================

def list_faiss_indices(base_dir="sources"):
    """
    Search through the sources directory and return the paths
    of all valid FAISS indexes.
    """

    faiss_dirs = []

    for root, dirs, files in os.walk(base_dir):

        # Check the CURRENT directory itself.
        #
        # This is slightly cleaner than looping through each
        # subdirectory and checking them separately.
        if is_valid_faiss_index(root):

            faiss_dirs.append(root)

    return faiss_dirs


# ============================================================
# 4. DISCOVER AVAILABLE INDEXES ONCE
# ============================================================

AVAILABLE_INDICES = list_faiss_indices("sources")

print("\n📚 Available FAISS indexes:")

for index_path in AVAILABLE_INDICES:
    print(f"   • {index_path}")

print()


# ============================================================
# 5. FAISS INDEX CACHE
# ============================================================

INDEX_CACHE = {}


def get_cached_index(index_path):
    """
    Return a FAISS index.

    If the index has already been loaded previously,
    return the copy stored in memory.

    Otherwise:
        1. Load the index from disk.
        2. Store it in INDEX_CACHE.
        3. Return it.
    """

    if index_path not in INDEX_CACHE:

        print(f"📥 Loading FAISS index into memory:")
        print(f"   {index_path}")

        INDEX_CACHE[index_path] = FAISS.load_local(
            index_path,
            embedding_model,
            allow_dangerous_deserialization=True
        )

    else:

        print(f"⚡ Using cached index:")
        print(f"   {index_path}")

    return INDEX_CACHE[index_path]


# ============================================================
# 6. SELECT THE BEST INDEX
# ============================================================

def select_best_index(query, k=4):
    """
    Search all available FAISS indexes and select the index
    whose best result has the smallest FAISS distance.

    Important:

    similarity_search_with_score() in your current setup is
    returning FAISS DISTANCES.

    Therefore:

        Smaller distance = better match

    Example:

        0.71  → better match
        1.44  → worse match
    """

    start_time = time.time()

    print("\n")
    print("=" * 60)
    print("🔍 STARTING INDEX SEARCH")
    print(f"Query: {query}")
    print("=" * 60)


    # --------------------------------------------------------
    # Variables that store the overall best source
    # --------------------------------------------------------

    best_score = float("inf")

    best_context = None

    best_index_path = None

    best_pages = []


    # --------------------------------------------------------
    # Search every available index
    # --------------------------------------------------------

    for index_path in AVAILABLE_INDICES:

        print()
        print(f"===== LOOKING IN {index_path} =====")

        try:

            # Get the index from memory if it was already loaded.
            #
            # Otherwise load it once from disk.
            db = get_cached_index(index_path)


            # Search for the top k chunks.
            results = db.similarity_search_with_score(
                query,
                k=k
            )


            # If somehow no results are returned, skip this index.
            if not results:

                print("⚠️ No results returned.")

                continue


            # ------------------------------------------------
            # Extract the FAISS distances
            # ------------------------------------------------

            scores = [
                score
                for _, score in results
            ]


            # The smallest distance is the strongest match
            min_score = min(scores)


            # The average distance gives us some information
            # about the general quality of the top results.
            avg_score = sum(scores) / len(scores)


            # ------------------------------------------------
            # PRINT RESULTS FOR DEBUGGING
            # ------------------------------------------------

            print(f"📂 {index_path}")

            print(f"Best distance: {min_score:.4f}")

            print(f"Average distance: {avg_score:.4f}")

            print()

            for document, score in results:

                preview = document.page_content[:100]

                preview = preview.replace("\n", " ")

                print(
                    f"   {score:.4f} => {preview}..."
                )


            # ------------------------------------------------
            # RELEVANCE THRESHOLD
            # ------------------------------------------------

            # This number should eventually be calibrated using
            # real test questions.
            #
            # Larger distance means less relevant.
            #
            # For now we preserve your existing threshold.

            MAX_DISTANCE = 1.2


            if min_score > MAX_DISTANCE:

                print(
                    f"❌ Rejected: best distance "
                    f"{min_score:.4f} is above "
                    f"threshold {MAX_DISTANCE}"
                )

                continue


            # ------------------------------------------------
            # CHECK WHETHER THIS INDEX IS BETTER
            # ------------------------------------------------

            if min_score < best_score:

                print("🏆 New best index!")

                best_score = min_score

                best_index_path = index_path


                # Combine the retrieved chunks into the context
                best_context = "\n".join(
                    document.page_content
                    for document, _ in results
                )


                # Extract page numbers from metadata
                best_pages = sorted(
                    {
                        document.metadata.get("page")

                        for document, _ in results

                        if document.metadata.get("page")
                        is not None
                    }
                )


        except Exception as e:

            print(
                f"⚠️ Failed to load or search "
                f"{index_path}"
            )

            print(f"Error: {e}")


    # ========================================================
    # FINISH TIMING
    # ========================================================

    duration = time.time() - start_time


    print()
    print("=" * 60)
    print("🏁 INDEX SEARCH COMPLETE")
    print("=" * 60)

    print(f"Best index: {best_index_path}")

    print(f"Best distance: {best_score}")

    print(f"Pages: {best_pages}")

    print(f"Retrieval time: {duration:.4f} seconds")

    print("=" * 60)
    print()


    # ========================================================
    # RETURN RESULTS
    # ========================================================

    return {

        "context": best_context,

        "best_index": best_index_path,

        "similarity_score": best_score,

        "pages": best_pages,

        "retrieval_duration": duration,
    }