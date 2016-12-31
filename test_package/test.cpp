#include "beanstalk.hpp"
#include <iostream>
#include <stdexcept>
#include <assert.h>

using namespace std;
using namespace Beanstalk;

int main() {
    try
    {
        Client client("127.0.0.1", 11300);
        assert(client.use("test"));
        assert(client.watch("test"));

        int id = client.put("hello");
        assert(id > 0);
        cout << "put job id: " << id << endl;

        Job job;
        assert(client.reserve(job) && job);
        assert(job.id() == id);

        cout << "reserved job id: "
             << job.id()
             << " with body {" << job.body() << "}"
             << endl;

        assert(client.del(job.id()));
        cout << "deleted job id: " << job.id() << endl;

    }
    catch(const runtime_error& e)
    {
         cout << e.what() << endl;
    }
}

