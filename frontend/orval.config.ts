import * as orval from "orval";

export default orval.defineConfig({
  api: {
    input: {
      target: "../schema/schema.yml",
    },
    output: {
      target: "./src/api/generated.ts",
      client: "react-query",
      override: {
        mutator: {
          path: "./src/utils/orval-mutator.ts",
          name: "orvalMutator",
        },
        query: {
          useQuery: true,
          signal: true,
        },
        operations: {
          "search-bookmarks": {
            query: {
              useQuery: true,
            },
          },
        },
      },
    },
  },
});
