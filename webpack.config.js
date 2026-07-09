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
                    MiniCssExtractPlugin.loader,
                    "css-loader",
                    "sass-loader",
                ],
            },
        ],
    },
    plugins: [
        new MiniCssExtractPlugin({
          filename: "css/[name].css", 
        }),
    ]
};
