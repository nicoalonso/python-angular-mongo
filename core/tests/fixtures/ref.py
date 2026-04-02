from enum import Enum


class Ref(Enum):
    # Authors
    AuthorShakespeare = 'author:shakespeare'
    AuthorCervantes = 'author:cervantes'
    # Books
    BookRomeoAndJuliet = 'book:romeo-and-juliet'
    BookDonQuijote = 'book:don-quijote'
    # Borrows
    BorrowJohnDoe = 'borrow:john-doe'
    # BorrowLines
    BorrowLineJohnRomeoAndJuliet = 'borrow-line:john-doe:romeo-and-juliet'
    BorrowLineJohnQuijote = 'borrow-line:john-doe:quijote'
    # Customers
    CustomerJohnDoe = 'customer:john-doe'
    # Editorials
    EditorialAnaya = 'editorial:anaya'
    # Providers
    ProviderAmazon = 'provider:amazon'
    ProviderBestBuy = 'provider:best-buy'
    # Purchases
    PurchaseAmazonInv1 = 'purchase:amazon:inv-1'
    PurchaseBestBuyInv2 = 'purchase:best-buy:inv-2'
    # PurchaseLines
    PurchaseLineAmazonLine1 = 'purchase-line:amazon:line1'
    PurchaseLineAmazonLine2 = 'purchase-line:amazon:line2'
    PurchaseLineBestBuyLine1 = 'purchase-line:best-buy:line1'
    # Sales
    SaleJohnDoe1 = 'sale:john-doe:1'
    SaleJohnDoe2 = 'sale:john-doe:2'
    # SaleLines
    SaleLineJohnDoe1Line1 = 'sale-line:john-doe:1:line-1'
    SaleLineJohnDoe1Line2 = 'sale-line:john-doe:1:line-2'
    SaleLineJohnDoe2Line1 = 'sale-line:john-doe:2:line-1'
    # Summaries
    SummaryDescription = 'summary:description'
    SummaryBiography = 'summary:biography'
