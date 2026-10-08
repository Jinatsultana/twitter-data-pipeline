let tweets = [];

Papa.parse("./data/refined_tweets.csv", {
    download: true,
    header: true,
    skipEmptyLines: true,

    complete: function (results) {

        tweets = results.data;

        console.log("CSV parsed successfully!");
        console.log("Total rows:", tweets.length);

        const userFilter = document.getElementById("userFilter");
        const filterResult = document.getElementById("filterResult");

        const tweetCount = document.getElementById("tweetCount");
        const likeCount = document.getElementById("likeCount");
        const shareCount = document.getElementById("shareCount");


        // -----------------------------------------
        // POPULATE USER FILTER
        // -----------------------------------------

        const users = [...new Set(
            tweets
                .map(tweet => tweet.user)
                .filter(user => user)
        )];

        users.sort();

        users.forEach(user => {

            const option = document.createElement("option");

            option.value = user;
            option.textContent = user;

            userFilter.appendChild(option);
        });

        console.log("User filter populated:", users.length);


        // -----------------------------------------
        // UPDATE ANALYTICS
        // -----------------------------------------

        function updateAnalytics(data, selectedUser) {

            let totalLikes = 0;
            let totalShares = 0;

            data.forEach(tweet => {

                const likes = Number(tweet.like_count) || 0;
                const shares = Number(tweet.share_count) || 0;

                totalLikes += likes;
                totalShares += shares;
            });


            tweetCount.textContent =
                data.length.toLocaleString();

            likeCount.textContent =
                totalLikes.toLocaleString();

            shareCount.textContent =
                totalShares.toLocaleString();


            if (selectedUser === "all") {

                filterResult.textContent =
                    "Showing all users";

            } else {

                filterResult.textContent =
    "Selected user: " + selectedUser;
            }
        }


        // -----------------------------------------
        // INITIAL ANALYTICS
        // -----------------------------------------

        updateAnalytics(tweets, "all");


        // -----------------------------------------
        // USER FILTER
        // -----------------------------------------

        userFilter.addEventListener("change", function () {

            const selectedUser = this.value;

            if (selectedUser === "all") {

                updateAnalytics(
                    tweets,
                    "all"
                );

            } else {

                const filteredTweets = tweets.filter(
                    tweet => tweet.user === selectedUser
                );

                updateAnalytics(
                    filteredTweets,
                    selectedUser
                );

                console.log(
                    "Selected user:",
                    selectedUser
                );

                console.log(
                    "Tweets:",
                    filteredTweets.length
                );
            }
        });
    },


    // -----------------------------------------
    // CSV ERROR
    // -----------------------------------------

    error: function (error) {

        console.error(
            "Error parsing CSV:",
            error
        );

    }
});