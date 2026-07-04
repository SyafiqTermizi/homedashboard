const path = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = {
    entry: {
        style: "./static/scss/index.scss",
    },
    output: {
        path: path.resolve("./static/build/"),
        filename: "[name].js",
    },
    module: {
        rules: [
            {
                test: /\.s[ac]ss$/i,
                use: [
                    // Creates `style` nodes from JS strings
                    MiniCssExtractPlugin.loader, 
                    // Translates CSS into CommonJS
                    "css-loader",
                    // Compiles Sass to CSS
                    "sass-loader",
                ],
            },
        ],
    },
    plugins: [
        // Extracts the compiled CSS into a standalone file in the output directory
        new MiniCssExtractPlugin({
          filename: 'css/[name].css', 
        }),
    ]
};