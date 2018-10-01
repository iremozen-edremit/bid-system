class tender:
    def __init__(self,timestamp, user_id,action, item, reserve_price, close_time):
        self.timestamp = timestamp
        self.user_id = user_id
        self.action = action
        self.item = item
        self.reserve_price = reserve_price
        self.close_time = close_time
        self.bid_list = []


class bid:
    def __init__(self,timestamp, user_id,action, item, bid_amount, isvalid):
        self.timestamp = timestamp
        self.user_id = user_id
        self.action = action
        self.item = item
        self.bid_amount = bid_amount
        self.isvalid = isvalid


fp = open('input.txt', 'r')
tender_list = []

for line in fp:
    line = line.split("|")
    line[0] = line[0].replace("\n", "")
    if len(line) >= 5:   # decided if it is bid/sell or just a timestamp
        if line[2] == 'SELL':
            tender_list.append(tender(line[0], line[1], line[2], line[3], line[4].replace("\n", ""), line[5].replace("\n", "")))

        if line[2] == 'BID':
            current_tender = [x for x in tender_list if x.item == str(line[3])] #select matched items
            # founded tender of a bid
            if len(current_tender)>0:
                #if this pid is valid for rules, append it to list
                if int(current_tender[0].close_time) >= int(line[0]) and float(current_tender[0].reserve_price)< float(line[4].replace("\n", "")): #if this conditions are provided then create a list which is about bids
                    previousBids = [y for y in current_tender[0].bid_list if y.user_id == line[1] and float(y.bid_amount) > float(line[4].replace("\n", ""))]
                    if len(previousBids) == 0: #if there is no bigger bids append to list and give True
                        current_tender[0].bid_list.append(bid(line[0], line[1], line[2], line[3], line[4].replace("\n", ""), True))
                    else:
                        current_tender[0].bid_list.append(bid(line[0], line[1], line[2], line[3], line[4].replace("\n", ""), False))
                else:
                    current_tender[0].bid_list.append(bid(line[0], line[1], line[2], line[3], line[4].replace("\n", ""), False))

    else:
        #chechk if any tenders ended
        finish_tender = [x for x in tender_list if int(x.close_time) == int(line[0])]
        #look to bids which belongs to tender and find the winner
        for tender in finish_tender:
            # Ture is validbids, False is unvalidbids
            validBids = [k for k in tender.bid_list if k.isvalid == True]

            if len(validBids)== 0:
                maxi = max(tender.bid_list, key=lambda x: float(x.bid_amount))
                mini = min(tender.bid_list, key=lambda x: float(x.bid_amount))
                print(tender.close_time, tender.item, 'UNSOLD','0', len(tender.bid_list), maxi.bid_amount, mini.bid_amount)
            elif len(validBids) == 1:
                print(tender.close_time, validBids[0].item, validBids[0].user_id, 'SOLD', tender.reserve_price )
            elif len(validBids) >= 2:
                maxi2 = max(tender.bid_list, key=lambda x: float(x.bid_amount))
                mini2 = min(tender.bid_list, key=lambda x: float(x.bid_amount))
                sortedBidlist =sorted(validBids, key=lambda x: (-float(x.bid_amount), x.timestamp))
                print(tender.close_time, sortedBidlist[0].item, sortedBidlist[0].user_id,'SOLD', sortedBidlist[1].bid_amount, len(tender.bid_list),
                      maxi2.bid_amount, mini2.bid_amount)











