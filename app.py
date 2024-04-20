from flask import Flask, render_template, request
import pickle
import numpy as np

popular_df = pickle.load(open('popular_df.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html',
                           book_name=popular_df['bookTitle'].to_list(),
                           author=popular_df['bookAuthor'].to_list(),
                           image=popular_df['imageUrlM'].to_list(),
                           votes=popular_df['numRating'].to_list(),
                           ratings=popular_df['avgRating'].to_list(),
                           )


@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')


@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')

    if user_input not in pt.index:
        error_message = "Book not found. Please try another book title."
        return render_template('recommend.html', error_message=error_message)

    index_ = np.where(pt.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index_])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['bookTitle'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('bookTitle')['bookTitle'].values))
        item.extend(list(temp_df.drop_duplicates('bookTitle')['bookAuthor'].values))
        item.extend(list(temp_df.drop_duplicates('bookTitle')['imageUrlM'].values))

        data.append(item)

    return render_template('recommend.html', data=data)


if __name__ == '__main__':
    app.run(debug=True)
